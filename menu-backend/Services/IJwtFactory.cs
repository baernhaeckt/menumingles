using backend.Api.Models;

namespace backend.Services;

public interface IJwtFactory
{
    string GenerateToken(User user);
}
