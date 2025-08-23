using Azure.Data.Tables;

namespace backend.Planning.Storage;

public class TablePlanSessionStore : IPlanSessionStore
{
    private readonly TableClient _table;

    public TablePlanSessionStore(TableServiceClient client)
    {
        _table = client.GetTableClient("Sessions");
        _table.CreateIfNotExists();
    }

    public async Task<string> StartSessionAsync(string householdKey, IEnumerable<string> startIngredients, string menus)
    {
        SessionEntity entity = new()
        {
            PartitionKey = householdKey,
            RowKey = Guid.NewGuid().ToString(),
            StartIngredients = string.Join(',', startIngredients),
            Menus = menus,
            CreatedAt = DateTimeOffset.UtcNow
        };
        await _table.AddEntityAsync(entity);
        return entity.RowKey;
    }
}
