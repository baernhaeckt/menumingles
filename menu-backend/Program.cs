using backend.Api.Endpoints;
using backend.Setup;

var builder = WebApplication.CreateBuilder(args);

// Register all services
builder.RegisterServices();

var app = builder.Build();

// Register all middlewares
app.RegisterMiddlewares();

// Register all endpoints
app.RegisterAuthEndpoints();

// Health check endpoint
app.MapGet("/health", () =>
{
    return Results.NoContent();
});

app.Run();

// Make the implicit Program class public so test projects can access it
public partial class Program { }