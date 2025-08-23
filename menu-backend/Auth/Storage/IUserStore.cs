using backend.Auth.Api;

namespace backend.Auth.Storage;

public interface IUserStore
{
    Task<User?> FindByUsernameAsync(string username);

    Task SaveAsync(User user, string password);

    Task<User?> VerifyPassword(string username, string password);
}