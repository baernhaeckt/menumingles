using Azure;
using Azure.Data.Tables;

namespace backend.Discussion.Storage;

public sealed class HouseholdEntity : ITableEntity
{
    // PartitionKey: householdkey (single partition)
    // RowKey: username (or user id)

    public required string PartitionKey { get; set; } = "HOUSEHOLD"; // householdkey
    
    public required string RowKey { get; set; } = default!; // householdkey

    public required string HouseholdKey { get; set; } = default!;

    public ETag ETag { get; set; }

    public DateTimeOffset? Timestamp { get; set; }

    public string People { get; set; }

    public string Chef { get; set; }

    public string Consultants { get; set; }

    public string Name { get; internal set; }
}
