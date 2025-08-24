using Azure;
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

    public async Task SaveMenuResultInProgress(string householdKey, string sessionKey, string taskId)
    {
        await _table.AddEntityAsync(new MenuResultEntity
        {
            PartitionKey = householdKey,
            RowKey = sessionKey,
            Result = null,
            TaskId = taskId,
            Timestamp = DateTimeOffset.UtcNow
        });
    }

    public async Task SaveMenuResult(string householdKey, string sessionKey, JsonElement result)
    {
        await _table.UpdateEntityAsync(new MenuResultEntity
        {
            PartitionKey = householdKey,
            RowKey = sessionKey,
            Result = JsonSerializer.Serialize(result),
            Timestamp = DateTimeOffset.UtcNow
        }, ETag.All, TableUpdateMode.Merge);
    }

    public async Task<MenuResult> GetAsync(string householdKey, string sessionKey)
    {
        MenuResultEntity entity = await _table.GetEntityAsync<MenuResultEntity>(householdKey, sessionKey);
        MenuResult result = new()
        {
            TaskId = entity.TaskId,
            Status = entity.Result == null ? MenuResultStatus.Pending : MenuResultStatus.Completed,
            Result = entity.Result == null ? null : JsonDocument.Parse(entity.Result)
        };
        return result;
    }


}