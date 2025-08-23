using Azure.Data.Tables;

using backend.Planning.Storage;

namespace backend.Planning;

public static class Registrar
{
    public static void RegisterPlanningServices(this WebApplicationBuilder builder)
    {
        builder.Services.AddSingleton<IPlanSessionStore, TablePlanSessionStore>();
        builder.Services.AddSingleton<TableServiceClient>(_ =>
        {
            var conn = builder.Configuration.GetConnectionString("TableStorage");
            return new TableServiceClient(conn);
        });
    }
}
