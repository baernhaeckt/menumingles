using Azure;
using Azure.Data.Tables;

namespace backend.Planning.Storage;

public sealed class SessionEntity : ITableEntity
{
    // PartitionKey: householdkey (single partition)
    // RowKey: username (or user id)

    public required string PartitionKey { get; set; } = default!; // householdkey
    
    public required string RowKey { get; set; } = default!; // username
 
    public required string HouseholdKey { get; set; } = default!;

    public ETag ETag { get; set; }

    public DateTimeOffset? Timestamp { get; set; }

    public required string StartIngredients { get; set; }

    public required string Menus { get; set; }

    public required DateTimeOffset CreatedAt { get; set; }
}

public sealed class SessionPartialForMatchUpdateEntity(string rowKey, string partitionKey, string matchedMenus) : ITableEntity
{
    public string PartitionKey { get; set; } = partitionKey;

    public string RowKey { get; set; } = rowKey;

    public DateTimeOffset? Timestamp { get; set; }

    public ETag ETag { get; set; }

    public string MatchedMenus { get; set; } = matchedMenus;
}
