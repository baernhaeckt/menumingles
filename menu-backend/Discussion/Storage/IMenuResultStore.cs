using System.Text.Json;

namespace backend.Discussion.Storage;

public interface IMenuResultStore
{
    Task SaveMenuResult(string householdKey, string sessionKey, JsonElement[] result);

    Task<MenuResult> GetAsync(string householdKey, string sessionKey);
}
