using Azure;
using Azure.Data.Tables;

using System.Text.Json;

namespace backend.Planning.Storage;

public class TablePlanSessionStore : IPlanSessionStore
{
    private readonly TableClient _table;

    public TablePlanSessionStore(TableServiceClient client)
    {
        _table = client.GetTableClient("Sessions");
        _table.CreateIfNotExists();
    }

    public async Task<Session> GetSessionAsync(string householdKey)
    {
        await foreach (Page<SessionEntity> page in _table
            .QueryAsync<SessionEntity>(e => e.PartitionKey == householdKey)
            .AsPages(pageSizeHint: 100))
        {
            if (page.Values.Count > 0)
            {
                SessionEntity entity = page.Values.OrderByDescending(session => session.CreatedAt).First();
                return new Session
                {
                    SessionKey = entity.RowKey,
                    HouseholdKey = entity.HouseholdKey,
                    MenuSelection = JsonDocument.Parse(entity.Menus),
                    MatchedMenus = JsonSerializer.Deserialize<IEnumerable<string>>(entity.MatchedMenus ?? "[]") ?? Array.Empty<string>(),
                };
            }
        }

        throw new KeyNotFoundException($"No session found for householdKey '{householdKey}'.");
    }

    public async Task<string> StartSessionAsync(string householdKey, IEnumerable<string> startIngredients, string menus)
    {
        SessionEntity entity = new()
        {
            PartitionKey = householdKey,
            RowKey = Guid.NewGuid().ToString(),
            StartIngredients = JsonSerializer.Serialize(startIngredients),
            Menus = menus,
            HouseholdKey = householdKey,
            CreatedAt = DateTimeOffset.UtcNow
        };
        await _table.AddEntityAsync(entity);
        return entity.RowKey;
    }

    public async Task StoreSessionSelectionAsync(string sessionKey, string householdKey, IEnumerable<string> matchedMenus)
    {
        await _table.UpdateEntityAsync(new SessionPartialForMatchUpdateEntity(sessionKey, householdKey, JsonSerializer.Serialize(matchedMenus)), ETag.All, TableUpdateMode.Merge);
    }
}
