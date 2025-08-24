
using backend.Auth.Api;

using System.Net;
using System.Net.Http.Headers;
using System.Net.Http.Json;

namespace backend.Tests.Integration;

[TestClass]
public class AuthEndpointTests
{
    private CustomWebApplicationFactory<Program> _factory = null!;

    [TestInitialize]
    public void Setup() => _factory = new CustomWebApplicationFactory<Program>();

    [TestCleanup]
    public void Cleanup() => _factory?.Dispose();

    [TestMethod]
    public async Task AuthRegisterEndpoint_ShouldReturn200Ok_WhenFreshHousehold()
    {
        // Arrange
        HttpClient client = _factory.CreateClient();

        // Act
        HttpResponseMessage response = await client.PostAsJsonAsync("/api/v1/auth/register", new RegisterRequest()
        {
            Username = "testuser",
            Email = "tester@test.ch",
            Password = "Test123",
            Household = "testhousehold"
        });

        // Assert
        Assert.AreEqual(HttpStatusCode.OK, response.StatusCode);
    }

    [TestMethod]
    public async Task AuthRegisterEndpoint_ShouldReturn200Ok_WhenExistingHousehold()
    {
        // Arrange
        HttpClient client = _factory.CreateClient();

        // Act
        HttpResponseMessage response = await client.PostAsJsonAsync("/api/v1/auth/register", new RegisterRequest()
        {
            Username = "testuser",
            Email = "tester@test.ch",
            Password = "Test123",
            Household = "testhousehold",
            HouseholdKey = "1234"
        });

        // Assert
        Assert.AreEqual(HttpStatusCode.OK, response.StatusCode);
    }

    [TestMethod]
    public async Task AuthLoginEndpoint_ShouldReturn200OkAndToken()
    {
        // Arrange
        HttpClient client = _factory.CreateClient();
        HttpResponseMessage response1 = await client.PostAsJsonAsync("/api/v1/auth/register", new RegisterRequest()
        {
            Username = "testuser",
            Email = "tester@test.ch",
            Password = "Test123",
            Household = "testhousehold"
        });
        response1.EnsureSuccessStatusCode();

        // Act
        HttpResponseMessage response2 = await client.PostAsJsonAsync("/api/v1/auth/login", new RegisterRequest()
        {
            Username = "testuser",
            Email = "tester@test.ch",
            Password = "Test123"
        });

        // Assert
        string token = await response2.Content.ReadAsStringAsync();
        Assert.AreEqual(HttpStatusCode.OK, response2.StatusCode);
    }

    [TestMethod]
    public async Task AuthMeEndpoint_ShouldReturn200OkAndUser()
    {
        // Arrange
        HttpClient client = _factory.CreateClient();
        HttpResponseMessage response1 = await client.PostAsJsonAsync("/api/v1/auth/register", new RegisterRequest()
        {
            Username = "testuser",
            Email = "tester@test.ch",
            Password = "Test123",
            Household = "testhousehold"
        });

        // Act
        HttpResponseMessage response = await client.PostAsJsonAsync("/api/v1/auth/login", new RegisterRequest()
        {
            Username = "testuser",
            Email = "tester@test.ch",
            Password = "Test123"
        });
        string token = await response.Content.ReadAsStringAsync();
        token = token.Replace("\"", "");
        client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);
        HttpResponseMessage meResponse = await client.GetAsync("/api/v1/auth/me");

        // Assert
        Assert.AreEqual(HttpStatusCode.OK, meResponse.StatusCode);
        ProfileResponse? responseContent = await meResponse.Content.ReadFromJsonAsync<ProfileResponse>();
        Assert.IsNotNull(responseContent?.HouseholdKey);
    }
}
