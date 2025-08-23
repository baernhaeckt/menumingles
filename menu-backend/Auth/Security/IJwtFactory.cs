using backend.Auth.Api;

namespace backend.Auth.Security;

public interface IJwtFactory
{
    string GenerateToken(User user);
}
