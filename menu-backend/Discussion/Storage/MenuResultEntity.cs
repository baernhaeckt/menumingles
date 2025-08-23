using Azure;
using Azure.Data.Tables;

namespace backend.Discussion.Storage;

public class MenuResultEntity : ITableEntity
{
    public string PartitionKey { get; set; }

    public string RowKey { get; set; }

    public string Result { get; set; }

    public ETag ETag { get; set; }

    public DateTimeOffset? Timestamp { get; set; }
}