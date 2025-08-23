using backend.Auth.Storage;
using backend.Discussion.Storage;

using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.Extensions.DependencyInjection;

namespace backend.Tests.Integration;

public class CustomWebApplicationFactory<TProgram>
    : WebApplicationFactory<TProgram> where TProgram : class
{
    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.ConfigureServices(services =>
        {
            var userStoreRegistration = services.SingleOrDefault(
                d => d.ServiceType ==
                    typeof(IUserStore));

            services.Remove(userStoreRegistration);

            services.AddSingleton<IUserStore, InMemoryUserStore>();

            var householdStoreRegistration = services.SingleOrDefault(
                d => d.ServiceType ==
                    typeof(IHouseholdStore));

            services.Remove(householdStoreRegistration);

            services.AddSingleton<IHouseholdStore, InMemoryHousholdStore>();
        });

        builder.UseEnvironment("Development");
    }
}
