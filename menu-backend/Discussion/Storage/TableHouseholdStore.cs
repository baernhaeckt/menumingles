using Azure.Data.Tables;

using System.Text.Json;

namespace backend.Discussion.Storage;

public class TableHouseholdStore : IHouseholdStore
{
    private readonly TableClient _table;

    public TableHouseholdStore(TableServiceClient client)
    {
        _table = client.GetTableClient("Households");
        _table.CreateIfNotExists();
    }

    public async Task CreateIfNotExistsAsync(string household, string householdKey)
    {
        var entity = await _table.GetEntityIfExistsAsync<HouseholdEntity>("HOUSEHOLD", householdKey, ["RowKey"]);
        if (entity.HasValue)
        {
            return;
        }

        _table.UpsertEntity(new HouseholdEntity
        {
            PartitionKey = "HOUSEHOLD",
            RowKey = householdKey,
            HouseholdKey = householdKey,
            Name = household,
            People = TemplateHouseholdPeople.People,
            Chef = TemplateChef.Chef,
            Consultants = TemplateConsultants.Consultants
        }, TableUpdateMode.Replace);
    }

    public async Task<Household> GetAsync(string householdKey)
    {
        return await _table.GetEntityAsync<HouseholdEntity>("HOUSEHOLD", householdKey)
            is { } entity
            ? new Household
            {
                HouseholdKey = entity.Value.RowKey,
                Name = entity.Value.Name,
                People = JsonDocument.Parse(entity.Value.People),
                Chef = JsonDocument.Parse(entity.Value.Chef),
                Consultants = JsonDocument.Parse(entity.Value.Consultants)
            }
            : throw new KeyNotFoundException($"Household with key '{householdKey}' not found.");
    }
}
