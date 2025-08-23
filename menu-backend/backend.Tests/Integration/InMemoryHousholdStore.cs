using backend.Discussion.Storage;

namespace backend.Tests.Integration;

public class InMemoryHousholdStore : IHouseholdStore
{
    public Task CreateIfNotExistsAsync(string household, string householdKey) => Task.CompletedTask;

    public Task<Household> GetAsync(string householdKey) => Task.FromResult(new Household());
}
