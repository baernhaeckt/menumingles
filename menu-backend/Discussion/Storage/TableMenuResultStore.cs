using Azure.Data.Tables;

using System.Text.Json;

namespace backend.Discussion.Storage;

public class TableMenuResultStore : IMenuResultStore
{
    private readonly TableClient _table;

    public TableMenuResultStore(TableServiceClient client)
    {
        _table = client.GetTableClient("MenuResults");
        _table.CreateIfNotExists();
    }
    public async Task SaveMenuResult(string householdKey, string sessionKey, JsonElement[] result)
    {
        await _table.AddEntityAsync(new MenuResultEntity
        {
            PartitionKey = householdKey,
            RowKey = sessionKey,
            Result = JsonSerializer.Serialize(result),
            Timestamp = DateTimeOffset.UtcNow
        });
    }

    public async Task<MenuResult> GetAsync(string householdKey, string sessionKey)
    {
        MenuResultEntity entity = await _table.GetEntityAsync<MenuResultEntity>(householdKey, sessionKey);
        return new MenuResult(
            JsonDocument.Parse(entity.Result)
        );
    }
}