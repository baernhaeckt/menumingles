using Azure;
using Azure.Data.Tables;

namespace backend.Planning.Storage;

public sealed class SessionEntity : ITableEntity
{
    // PartitionKey: householdkey (single partition)
    // RowKey: username (or user id)

    public string PartitionKey { get; set; } = default!; // householdkey
    
    public string RowKey { get; set; } = default!; // username
 
    public string HouseholdKey { get; set; } = default!;

    public ETag ETag { get; set; }

    public DateTimeOffset? Timestamp { get; set; }
    public string StartIngredients { get; internal set; }
    public string Menus { get; internal set; }
    public DateTimeOffset CreatedAt { get; internal set; }
}
