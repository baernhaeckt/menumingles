namespace backend.Auth.Storage;

using Azure.Data.Tables;

using backend.Auth.Api;

using System.Security.Cryptography;

public sealed class TableUserStore : IUserStore
{
    private readonly TableClient _table;

    public TableUserStore(TableServiceClient client)
    {
        _table = client.GetTableClient("Users");
        _table.CreateIfNotExists();
    }

    public async Task<User?> FindByUsernameAsync(string username)
    {
        var entity = await _table.GetEntityIfExistsAsync<UserEntity>("USER", username);
        if (entity.HasValue is false)
        {
            return null;
        }

        UserEntity? value = entity.Value;
        return new User(value.RowKey, value.Email, value.Household, value.HouseholdKey);
    }

    public async Task<User?> VerifyPassword(string username, string password)
    {
        var entity = await _table.GetEntityIfExistsAsync<UserEntity>("USER", username);
        if (!entity.HasValue)
        {
            return null;
        }

        UserEntity value = entity.Value!;
        byte[] storedHash = Convert.FromBase64String(value.PasswordHash);
        byte[] storedSalt = Convert.FromBase64String(value.PasswordSalt);
        if (!CryptographicOperations.FixedTimeEquals(storedHash, Hash(password, storedSalt)))
        {
            return null;
        }

        return new User(value.RowKey, value.Email, value.Household, value.HouseholdKey);
    }

    public async Task SaveAsync(User user, string password)
    {
        byte[] salt = RandomNumberGenerator.GetBytes(16);
        var entity = new UserEntity
        {
            RowKey = user.Username,
            Email = user.Email,
            PasswordSalt = Convert.ToBase64String(salt),
            PasswordHash = Convert.ToBase64String(Hash(password, salt)),
            Household = user.Household,
            HouseholdKey = user.HouseholdKey
        };
        await _table.UpsertEntityAsync(entity);
    }

    private static byte[] Hash(string pwd, byte[] salt)
    {
        using var pbkdf2 = new Rfc2898DeriveBytes(pwd, salt, 100_000, HashAlgorithmName.SHA256);
        return pbkdf2.GetBytes(32);
    }
}
