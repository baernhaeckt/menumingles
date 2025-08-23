
namespace backend.Discussion.Storage
{
    public interface IHouseholdStore
    {
        Task CreateIfNotExistsAsync(string household, string householdKey);

        Task<Household> GetAsync(string householdKey);
    }
}