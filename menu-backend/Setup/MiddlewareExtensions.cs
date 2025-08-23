namespace backend.Setup;

public static class MiddlewareExtensions
{
    public static void RegisterMiddlewares(this WebApplication app)
    {
        // Add Docs
        app.UseSwagger();
        app.UseSwaggerUI(c =>
        {
            c.RoutePrefix = "docs";
        });

        // Enforece HTTPS
        app.UseHttpsRedirection();

        // Add authentication and authorization
        app.UseAuthentication();
        app.UseAuthorization();

        // Serve OpenAPI JSON
        app.MapOpenApi();
    }
}
