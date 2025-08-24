using Microsoft.AspNetCore.Mvc.Testing;

using System.Net;

namespace backend.Tests.Integration;

[TestClass]
public class HealthEndpointTests
{
    private WebApplicationFactory<Program> _factory = null!;

    [TestInitialize]
    public void Setup() => _factory = new WebApplicationFactory<Program>();

    [TestCleanup]
    public void Cleanup() => _factory?.Dispose();

    [TestMethod]
    public async Task HealthEndpoint_ShouldReturn204NoContent()
    {
        // Arrange
        HttpClient client = _factory.CreateClient();

        // Act
        HttpResponseMessage response = await client.GetAsync("/health");

        // Assert
        Assert.AreEqual(HttpStatusCode.NoContent, response.StatusCode);
    }
}
