namespace backend.Planning.Storage;

public interface IPlanSessionStore
{
    Task<string> StartSessionAsync(string householdKey, IEnumerable<string> startIngredients, string menus);
}
