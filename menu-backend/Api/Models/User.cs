namespace backend.Api.Models;

public class User
{
    public User(string username, string email, string household, string householdKey)
    {
        Username = username;
        Email = email;
        Household = household;
        HouseholdKey = householdKey;
    }

    public string Username { get; set; } = string.Empty;

    public string Email { get; set; } = string.Empty;

    public string HouseholdKey { get; set; } = string.Empty;

    public string Household { get; set; } = string.Empty;
}
