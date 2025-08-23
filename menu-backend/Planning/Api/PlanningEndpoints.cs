using backend.Common;
using backend.Planning.Storage;

using Microsoft.AspNetCore.Mvc;

using System.Security.Claims;

namespace backend.Planning.Api;

public static class PlanningEndpoints
{
    public static void RegisterPlanningEndpoints(this IEndpointRouteBuilder routes)
    {
        var plan = routes.MapGroup("/api/v1/planning");

        // Start planning session endpoint
        plan.MapPost("/start", async (
            [FromBody] PlanningStartRequest request,
            IPlanSessionStore planSessionStore,
            RecommenderClient recommenderClient,
            ClaimsPrincipal user) =>
        {
            // We get from the ingredients we have from the fridge a recommendation for starting menus
            var result = await recommenderClient.RecommendAsync(request.Ingredients);

            // We start a planning session with the user household key, the ingredients and the recommended menus
            // When a user from this household logs in, he can continue this session and plan a menue
            string sessionKey = await planSessionStore.StartSessionAsync(user.GetHouseholdKey(), request.Ingredients, result.RootElement.GetRawText());

            // We notify the users that the planning session has started (i.e., the fridge send a msg)
            // TODO: REST API to send notification into the chat (other system has websocket)

            return Results.Ok(sessionKey);
        })
        .WithName("Start")
        .WithOpenApi()
        .WithTags("Plan")
        .RequireAuthorization();

        // Continue planning session endpoint
        plan.MapPost("/continue", async (
            IPlanSessionStore planSessionStore,
            ClaimsPrincipal user) =>
        {
            string houseHoldKey = user.GetHouseholdKey();

            // There is a session for this household, get it to continue
            Session session = await planSessionStore.GetSessionAsync(houseHoldKey);

            return Results.Ok(new ContinueResponse
            {
                SessionKey = session.SessionKey,
                MenuSelection = session.MenuSelection
            });
        })
        .WithName("Continue")
        .WithOpenApi()
        .WithTags("Plan")
        .RequireAuthorization();


        // Menu selection made endpoint
        plan.MapPost("/selection", async (
            [FromBody] SelectionRequest request,
            IPlanSessionStore planSessionStore,
            ClaimsPrincipal user) =>
        {
            string houseHoldKey = user.GetHouseholdKey();

            await planSessionStore.StoreSessionSelectionAsync(
                request.SessionKey,
                user.GetHouseholdKey(),
                request.MatchedMenus);

            return Results.NoContent();
        })
        .WithName("Selection")
        .WithOpenApi()
        .WithTags("Plan")
        .RequireAuthorization();
    }
}
