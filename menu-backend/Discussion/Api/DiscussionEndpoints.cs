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

        // Start discussion for planned session endpoint
        discuss.MapPost("/start", async (
            [FromBody] DiscussionStartRequest request,
            IHouseholdStore householdStore,
            IPlanSessionStore sessionStore,
            MenuMinglersClient menuMinglersClient,
            ClaimsPrincipal user) =>
        {
            Household household = await householdStore.GetAsync(user.GetHouseholdKey());
            Session session = await sessionStore.GetSessionAsync(user.GetHouseholdKey());
            JsonElement[] selectedMenus = session.MenuSelection.RootElement
                .EnumerateArray()
                .Where(
                    x => session.MatchedMenus.Contains(x.GetProperty("name").GetString()))
                .ToArray();


            CancellationTokenSource cancellationTokenSource = new();
            cancellationTokenSource.CancelAfter(TimeSpan.FromMinutes(5));

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
            .ContinueWith(response =>
            {
                return response.Result;
            });

            return Results.NoContent();
        })
        .WithName("StartDiscussion")
        .WithOpenApi()
        .WithTags("Discussion")
        .RequireAuthorization();
    }
}

public class DiscussionStartRequest
{
    public string SessionKey { get; set; } = default!;
}
