var builder = WebApplication.CreateBuilder(args);

builder.Services.AddOpenApi();
builder.Services.AddEndpointsApiExplorer();

builder.Services.AddSwaggerGen(o =>
{
    o.SwaggerDoc("v1", new() { Title = "MenuMingles API", Version = "v1" });
});

var app = builder.Build();

// Serve OpenAPI JSON at /docs/v1/swagger.json and UI at /docs
app.UseSwagger(c =>
{
    c.RouteTemplate = "docs/{documentName}/swagger.json";
});
app.UseSwaggerUI(c =>
{
    c.RoutePrefix = "docs";
    c.SwaggerEndpoint("/docs/v1/swagger.json", "MenuMingles API v1");
});

app.MapOpenApi();

app.UseHttpsRedirection();

app.MapGet("/health", () =>
{
    return Results.NoContent();
});

app.Run();

public partial class Program { }