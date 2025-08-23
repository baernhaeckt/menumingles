using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;

using backend.Api.Models;

using Microsoft.IdentityModel.Tokens;

namespace backend.Services;

public class JwtFactory : IJwtFactory
{
    private readonly IConfiguration _configuration;
    private readonly SymmetricSecurityKey _key;

    public JwtFactory(IConfiguration configuration)
    {
        _configuration = configuration;
        var jwtKey = _configuration["Jwt:Key"] ?? throw new InvalidOperationException("JWT Key not configured");
        _key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(jwtKey));
    }

    public string GenerateToken(User user)
    {
        var tokenHandler = new JwtSecurityTokenHandler();
        var claims = new[]
        {
            new Claim(ClaimTypes.NameIdentifier, user.Username),
            new Claim(ClaimTypes.Name, user.Username),
            new Claim(ClaimTypes.Email, user.Email)
        };

        var tokenDescriptor = new SecurityTokenDescriptor
        {
            Subject = new ClaimsIdentity(claims),
            Expires = DateTime.UtcNow.AddHours(48),
            SigningCredentials = new SigningCredentials(_key, SecurityAlgorithms.HmacSha256Signature),
            Issuer = _configuration["Jwt:Issuer"],
            Audience = _configuration["Jwt:Audience"]
        };

        var token = tokenHandler.CreateToken(tokenDescriptor);
        return tokenHandler.WriteToken(token);
    }
}
