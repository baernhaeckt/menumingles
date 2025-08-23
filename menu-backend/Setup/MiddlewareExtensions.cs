namespace backend.Setup;

public static class MiddlewareExtensions
{
    public static void RegisterMiddlewares(this WebApplication app)
    {
        app.UseSwagger();
        app.UseSwaggerUI(c =>
        {
            c.SwaggerEndpoint("/swagger/v1/swagger.json", "MenuMingles API v1");
            c.RoutePrefix = "docs";
        });

        if (app.Environment.IsDevelopment())
        {
            //app.UseHttpsRedirection();
        }

        // Add authentication and authorization
        app.UseAuthentication();
        app.UseAuthorization();

        // Serve OpenAPI JSON
        app.MapOpenApi();
    }
}
