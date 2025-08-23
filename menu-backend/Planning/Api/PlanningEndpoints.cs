using backend.Common;
using backend.Planning.Storage;

using Microsoft.AspNetCore.Mvc;

namespace backend.Planning.Api;

public static class PlanningEndpoints
{
    public static void RegisterPlanningEndpoints(this IEndpointRouteBuilder routes)
    {
        var auth = routes.MapGroup("/api/v1/planning");

        // Start planning session endpoint
        auth.MapPost("/start", async (
            [FromBody] PlanningStartRequest request,
            IPlanSessionStore planSessionStore,
            RecommenderClient recommenderClient) =>
        {
            var result = await recommenderClient.RecommendAsync(request.Ingredients);
            return Results.Ok(result);
        })
        .WithName("Start")
        .WithOpenApi()
        .WithTags("Plan");

    }
}

public class PlanningStartRequest
{
    public string HouseholdKey { get; set; }

    public IEnumerable<string> Ingredients { get; set; }
}
