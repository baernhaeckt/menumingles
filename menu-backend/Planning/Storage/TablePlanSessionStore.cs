using Azure.Data.Tables;

namespace backend.Planning.Storage;

public class TablePlanSessionStore : IPlanSessionStore
{
    private readonly TableClient _table;

    public TablePlanSessionStore(TableServiceClient client)
    {
        _table = client.GetTableClient("Sessions");
        _table.CreateIfNotExists();
    }

    public void StartSession(string householdKey, IEnumerable<string> startIngredients)
    {
        TableEntity entity = new(householdKey, Guid.NewGuid().ToString())
        {
            { "StartTime", DateTime.UtcNow },
            { "IsActive", true }
        };
        _table.AddEntity(entity);
    }


}
