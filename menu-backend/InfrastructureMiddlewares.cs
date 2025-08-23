namespace backend;

public static class InfrastructureMiddlewares
{
    public static void RegisterMiddlewares(this WebApplication app)
    {
        // Add Docs
        app.UseSwagger();
        app.UseSwaggerUI();

        // Enforece HTTPS
        if (!app.Environment.IsDevelopment())
        {
            app.UseHttpsRedirection();
        }

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
