namespace backend.Auth.Storage;

using Azure;
using Azure.Data.Tables;

public sealed class UserEntity : ITableEntity
{
    // PartitionKey: "USER" (single partition)
    // RowKey: username (or user id)

    public string PartitionKey { get; set; } = "USER";

    public string RowKey { get; set; } = default!; // username

    public string Email { get; set; } = default!;

    public string Household { get; set; } = default!;

    public string HouseholdKey { get; set; } = default!;

    public ETag ETag { get; set; }

    public DateTimeOffset? Timestamp { get; set; }

    public required string PasswordSalt { get; set; }

    public required string PasswordHash { get; set; }
}
