using backend.Api.Models;
using backend.Services;
using backend.Storage;

using Microsoft.AspNetCore.Mvc;

namespace backend.Api.Endpoints;

public static class AuthEndpoints
{
    public static void RegisterAuthEndpoints(this IEndpointRouteBuilder routes)
    {
        var auth = routes.MapGroup("/api/v1/auth");

        // Login endpoint
        auth.MapPost("/login", async (
            [FromBody] LoginRequest request,
            IUserStore userStore,
            IJwtFactory jwtService) =>
        {
            if (string.IsNullOrEmpty(request.Username) || string.IsNullOrEmpty(request.Password))
            {
                return Results.BadRequest(new { message = "Username and password are required" });
            }

            User? user = await userStore.VerifyPassword(request.Username, request.Password);
            if (user == null)
            {
                return Results.Unauthorized();
            }

            string token = jwtService.GenerateToken(user);

            return Results.Ok(token);
        })
        .WithName("Login")
        .WithOpenApi()
        .WithTags("Authentication");

        // Register endpoint
        auth.MapPost("/register", async (
            [FromBody] RegisterRequest request,
            IUserStore userStore) =>
        {
            if (string.IsNullOrEmpty(request.Username) || 
                string.IsNullOrEmpty(request.Email) || 
                string.IsNullOrEmpty(request.Password))
            {
                return Results.BadRequest(new { message = "All fields are required" });
            }

            if (request.Password.Length < 4)
            {
                return Results.BadRequest(new { message = "Password must be at least 4 characters long" });
            }

            User? user = await userStore.FindByUsernameAsync(request.Username);

            if (user != null)
            {
                return Results.BadRequest(new { message = "Username or email already exists" });
            }

            await userStore.SaveAsync(new User(request.Username, request.Email), request.Password);

            return Results.Ok(new { message = "User registered successfully" });
        })
        .WithName("Register")
        .WithOpenApi()
        .WithTags("Authentication");

        // Get current user endpoint (protected)
        auth.MapGet("/me", async (
            HttpContext context,
            IUserStore userStore) =>
        {
            string? username = context.User.Identity?.Name;
            if (string.IsNullOrEmpty(username))
            {
                return Results.Unauthorized();
            }

            User? user = await userStore.FindByUsernameAsync(username);
            if (user == null)
            {
                return Results.NotFound();
            }

            return Results.Ok(new
            {
                user.Username,
                user.Email
            });
        })
        .WithName("GetCurrentUser")
        .WithOpenApi()
        .WithTags("Authentication")
        .RequireAuthorization();
    }
}
