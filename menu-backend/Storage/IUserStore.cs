using backend.Api.Models;

namespace backend.Storage;

public interface IUserStore
{
    Task<User?> FindByUsernameAsync(string username);

    Task SaveAsync(User user, string password);

    Task<User?> VerifyPassword(string username, string password);
}