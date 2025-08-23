namespace backend.Api.Models;

public class RegisterRequest
{
    public string Username { get; set; } = string.Empty;
    
    public string Email { get; set; } = string.Empty;

    public string Password { get; set; } = string.Empty;

    public string Household { get; set; } = string.Empty;

    public string? HouseholdKey { get; set; } = null;
}
