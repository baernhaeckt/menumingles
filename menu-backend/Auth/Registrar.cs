using Azure.Data.Tables;

using backend.Auth.Security;
using backend.Auth.Storage;

namespace backend.Auth;

public static class Registrar
{
    public static void RegisterAuthServices(this WebApplicationBuilder builder)
    {
        builder.Services.AddScoped<IJwtFactory, JwtFactory>();
        builder.Services.AddSingleton<IUserStore, TableUserStore>();
        builder.Services.AddSingleton<TableServiceClient>(_ =>
        {
            var conn = builder.Configuration.GetConnectionString("TableStorage");
            return new TableServiceClient(conn);
        });
    }
}
