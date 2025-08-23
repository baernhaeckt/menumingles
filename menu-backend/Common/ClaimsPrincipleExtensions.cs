using System.Security.Claims;

namespace backend.Common;

public static class ClaimsPrincipalExtensions
{
    /// <summary>
    /// Extracts the household key from the ClaimsPrincipal.
    /// Returns <c>null</c> if the claim is not present.
    /// </summary>
    public static string GetHouseholdKey(this ClaimsPrincipal user)
    {
        ArgumentNullException.ThrowIfNull(user);
        string? key = user.FindFirstValue(MenuMinglesClaims.HouseholdKey);
        if (key == null)
        {
            throw new ArgumentException("HouseholdKey claim is missing");
        }
        return key;
    }
}
