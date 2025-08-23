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
            ClaimsPrincipal user) =>
        {
            Household household = await householdStore.GetAsync(user.GetHouseholdKey());
            Session session = await sessionStore.GetSessionAsync(user.GetHouseholdKey());

            // We need to get the menu with ingriedients based on the matching process
            // From the matching process we only got the names, thus we resovle them here
            JsonElement[] selectedMenus = [.. session.MenuSelection.RootElement
                .EnumerateArray()
                .Where(
                    x => session.MatchedMenus.Contains(x.GetProperty("name").GetString()))];

            CancellationTokenSource cancellationTokenSource = new();
            cancellationTokenSource.CancelAfter(TimeSpan.FromMinutes(5));

            // TODO: Remove, this is for debugging purposes only
            var output = JsonSerializer.Serialize(new DiscussionRequest(
               household.People,
                household.Chef!,
                household.Consultants!,
                selectedMenus));

            // Fire and forget that, to return to the UI
#pragma warning disable CS4014 // Because this call is not awaited, execution of the current method continues before the call is completed
            menuMinglersClient
            .DiscussAsync(new DiscussionRequest(
               household.People,
                household.Chef!,
                household.Consultants!,
                selectedMenus), cancellationTokenSource.Token
#pragma warning restore CS4014 // Because this call is not awaited, execution of the current method continues before the call is completed
            )
            .ContinueWith(async response =>
            {
                await menuResultStore.SaveMenuResult(session.HouseholdKey, session.SessionKey, response.Result!.Results);
                return response.Result;
            });

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
            return Results.Ok(menuResult);
        })
        .WithName("ResultDiscussion")
        .WithOpenApi()
        .WithTags("Discussion")
        .RequireAuthorization();
    }
}
