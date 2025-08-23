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
        var plan = routes.MapGroup("/api/v1/discussion");

        // Start discussion for planned session endpoint
        plan.MapPost("/begin", async (
            [FromBody] DiscussionStartRequest request,
            IHouseholdStore householdStore,
            IPlanSessionStore sessionStore,
            MenuMinglersClient menuMinglersClient,
            ClaimsPrincipal user) =>
        {
            Household household = await householdStore.GetAsync(user.GetHouseholdKey());
            Session session = await sessionStore.GetSessionAsync(user.GetHouseholdKey());

            // Fire and forget that, to return to the UI
            menuMinglersClient
            .DiscussAsync(new DiscussionRequest(
                JsonSerializer.Deserialize<List<TinyPerson>>(household.People)!,
                JsonSerializer.Deserialize<Chef>(household.Chef)!,
                JsonSerializer.Deserialize<List<Consultant>>(household.Consultants)!,
                JsonSerializer.Deserialize<List<MenuItem>>(session.MenuSelection)!)
            )
            .ContinueWith(response =>
            {
                return response.Result;
            });

            return Results.NoContent();
        })
        .WithName("Begin")
        .WithOpenApi()
        .WithTags("Plan")
        .RequireAuthorization();
    }
}

public class DiscussionStartRequest
{
    public string SessionKey { get; set; } = default!;
}
