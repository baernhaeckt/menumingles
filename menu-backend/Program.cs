using backend;
using backend.Auth;
using backend.Auth.Api;
using backend.Planning;
using backend.Planning.Api;

var builder = WebApplication.CreateBuilder(args);

// Register all services
builder.RegisterInfrastructureServices();

// Register all features
builder.RegisterAuthServices();
builder.RegisterPlanningServices();

var app = builder.Build();

// Register all middlewares
app.RegisterMiddlewares();

// Register all endpoints
app.RegisterAuthEndpoints();
app.RegisterPlanningEndpoints();

// Health check endpoint
app.MapGet("/health", () =>
{
    return Results.NoContent();
});

app.Run();

// Make the implicit Program class public so test projects can access it
public partial class Program { }