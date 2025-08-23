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
            var result = await recommenderClient.RecommendAsync(request.Ingredients);
            string sessionKey = await planSessionStore.StartSessionAsync(user.GetHouseholdKey(), request.Ingredients, result.RootElement.GetRawText());
            return Results.Ok(sessionKey);
        })
        .WithName("Start")
        .WithOpenApi()
        .WithTags("Plan")
        .RequireAuthorization();
    }
}
