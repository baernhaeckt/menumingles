using Azure;
using Azure.Data.Tables;

namespace backend.Discussion.Storage;

public class MenuResultEntity : ITableEntity
{
    public required string PartitionKey { get; set; }

    public required string RowKey { get; set; }

    public string? Result { get; set; }

    public ETag ETag { get; set; }

    public DateTimeOffset? Timestamp { get; set; }

    public string? TaskId { get; set; }
}