using backend.Discussion.Storage;

using System.Text.Json;

namespace backend.Tests.Integration;

public class InMemoryHousholdStore : IHouseholdStore
{
    public Task CreateIfNotExistsAsync(string household, string householdKey) => Task.CompletedTask;

    public Task<Household> GetAsync(string householdKey) => Task.FromResult(new Household
    {
        HouseholdKey = "",
        Name = "",
        People = JsonDocument.Parse(TemplateHouseholdPeople.People),
        Chef = JsonDocument.Parse(TemplateChef.Chef),
        Consultants = JsonDocument.Parse(TemplateConsultants.Consultants)
    });
}
