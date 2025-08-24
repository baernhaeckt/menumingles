using backend.Common;
using backend.Discussion.Storage;
using backend.Planning.Storage;

using Microsoft.AspNetCore.Mvc;

using System.Security.Claims;
using System.Text.Json;

namespace backend.Discussion.Api;

public static class DiscussionEndpoints
{
    public static void RegisterDiscussionEndpoints(this IEndpointRouteBuilder routes)
    {
        var discuss = routes.MapGroup("/api/v1/discussion");

        // Start discussion of mingles for the pre planned session
        discuss.MapPost("/start", async (
            [FromBody] DiscussionStartRequest request,
            IHouseholdStore householdStore,
            IPlanSessionStore sessionStore,
            IMenuResultStore menuResultStore,
            MenuMinglersClient menuMinglersClient,
            RecommenderClient recommenderClient,
            ClaimsPrincipal user) =>
        {
            Household household = await householdStore.GetAsync(user.GetHouseholdKey());
            Session session = await sessionStore.GetSessionAsync(user.GetHouseholdKey());

            // We need to get the menu with ingriedients based on the matching process
            // From the matching process we only got the names, thus we resovle them here.
            // From the ingriedients, we generate menus to discuss.
            IEnumerable<string> ingredientsOfMenus = session.MenuSelection.RootElement
                .EnumerateArray()
                .Where(
                    x => session.MatchedMenus.Contains(x.GetProperty("name").GetString()))
                .SelectMany(x => x.GetProperty("ingredients").GetString().Split(", "))
                .Where(x => x is not null)
                .Distinct()
                .ToArray();
            JsonDocument menusToDiscuss = await recommenderClient.RecommendAsync(ingredientsOfMenus, 12);

            // Conversation takes some time, so we do this in the background and let the UI poll
            DiscussionTaskResponse? result = await menuMinglersClient.DiscussAsync(new DiscussionRequest(
               household.People,
                household.Chef!,
                household.Consultants!,
                menusToDiscuss.RootElement.EnumerateArray().ToArray())
            );

            string taskId = result?.TaskId ?? throw new InvalidOperationException("TaskId required.");
            await menuResultStore.SaveMenuResultInProgress(user.GetHouseholdKey(), request.SessionKey, taskId);

            return Results.NoContent();
        })
        .WithName("StartDiscussion")
        .WithOpenApi()
        .WithTags("Discussion")
        .RequireAuthorization();

        // Result of discussion, call this to see if the result is completed
        discuss.MapPost("/result", async (
            [FromBody] DiscussionResultRequest request,
            IMenuResultStore menuResultStore,
            MenuMinglersClient menuMinglersClient,
            ClaimsPrincipal user) =>
        {
            MenuResult menuResult = await menuResultStore.GetAsync(user.GetHouseholdKey(), request.SessionKey);
            if (menuResult.Status == MenuResultStatus.Pending)
            {
                DiscussionStatusResponse? discussionStatusResponse = await menuMinglersClient.GetDiscussionStatusAsync(menuResult.TaskId);
                if (discussionStatusResponse is not null && discussionStatusResponse.Result is not null)
                {
                    JsonElement result = discussionStatusResponse.Result.Value;
                    await menuResultStore.SaveMenuResult(user.GetHouseholdKey(), request.SessionKey, result);
                }
            }

            return Results.Ok(new DiscussionResultResponse(menuResult.Status, menuResult.Result));
        })
        .WithName("ResultDiscussion")
        .WithOpenApi()
        .WithTags("Discussion")
        .RequireAuthorization();
    }
}
