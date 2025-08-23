using System.Text.Json;

namespace backend.Planning.Storage;

public interface IPlanSessionStore
{
    Task<string> StartSessionAsync(string householdKey, IEnumerable<string> startIngredients, string menus);

    Task<Session> GetSessionAsync(string householdKey);

    Task StoreSessionSelectionAsync(string sessionKey, string householdKey, IEnumerable<string> matchedMenus);
}
