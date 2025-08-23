using Azure.Data.Tables;

using backend.Discussion.Storage;

namespace backend.Discussion;

public static class Registrar
{
    public static void RegisterHouseholdServices(this WebApplicationBuilder builder)
    {
        builder.Services.AddSingleton<IHouseholdStore, TableHouseholdStore>();
        builder.Services.AddSingleton<IMenuResultStore, TableMenuResultStore>();
        builder.Services.AddSingleton(_ =>
        {
            var conn = builder.Configuration.GetConnectionString("TableStorage");
            return new TableServiceClient(conn);
        });
    }
}
