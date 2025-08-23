namespace backend.Setup;

public static class MiddlewareExtensions
{
    public static void RegisterMiddlewares(this WebApplication app)
    {
        // Add Docs
        app.UseSwagger();
        app.UseSwaggerUI(c =>
        {
            c.SwaggerEndpoint("/swagger/v1/swagger.json", "MenuMingles API");
            c.RoutePrefix = "docs";
        });

        // Enforece HTTPS
        app.UseHttpsRedirection();

        // Add authentication and authorization
        app.UseAuthentication();
        app.UseAuthorization();

        app.UseCors(x =>
        {
            x.AllowAnyMethod()
                .WithOrigins(
                    "http://localhost:5173/",
                    "https://menu-mingles-frontend-cccnfba0ezc2dhbc.northeurope-01.azurewebsites.net/")
                .AllowAnyHeader()
                .WithExposedHeaders("Authorization")
                .AllowCredentials();
        });

        // Serve OpenAPI JSON
        app.MapOpenApi();
    }
}
