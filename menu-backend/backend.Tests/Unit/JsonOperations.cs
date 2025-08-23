using System.Text.Json;

namespace backend.Tests.Unit;

[TestClass]
public class JsonOperations
{
    [TestMethod]
    public void ShouldParseJson()
    {
        // Arrange
        var menus = JsonDocument.Parse("""[{"name":"Drunk Wienies","ingredients":"vinegar, sugar, beer, tomato paste, wienies, chili powder, onion, cooking oil, garlic powder, paprika, dry mustard, worcestershire sauce"},{"name":"Slow Cooker Root Veggie Winter Soup","ingredients":"caraway seeds, white onion, cilantro, parsnips, coriander seeds, green onion, water, ground white pepper, chicken broth, tarragon, colored carrots, vegetable broth"},{"name":"Sauteed Baby Artichokes ","ingredients":"lemon juice, parmesan cheese, baby artichokes, pancetta, mint leaves, freshly ground black pepper, white wine, garlic, olive oil, salt"},{"name":"Mom\u0027S Marinated Flank Steak","ingredients":"soy sauce, lemon juice, brown sugar, green onion, flank steak, beef broth, salt"},{"name":"Mild Crock Pot Chili","ingredients":"kidney beans, sour cream, ground cumin, tomatoes, taco, chili powder, cheddar cheese, onion, tomato soup, lean ground beef, great northern beans, tomato sauce"},{"name":"Chocolate Chip Angel Cupcakes With Fluffy Frosting","ingredients":"cake flour, sugar, vanilla, chocolate minichips, lemon juice, remaining ingredient, frosting, egg whites, water, coconut, cream of tartar, salt"},{"name":"Cranberry-Black Bean Relish","ingredients":"black beans, salt, cranberries, lime juice, honey, olive oil, fresh cilantro"},{"name":"Stacy\u0027S Greek-Inspired Tuna Salad","ingredients":"spring mix greens, lemon juice, red grapes, pita chips, tzatziki sauce, fresh dill, feta cheese crumbles, cucumber, white albacore, almonds, salt"},{"name":"Double Delicious Almond Cookies","ingredients":"egg, baking powder, sugar, almond, flour, almonds, butter, salt"},{"name":"Asian Taro Tapioca Dessert Soup","ingredients":"condensed milk, taro root, tapioca, unsweetened coconut milk"},{"name":"Salmon Dyonnaise","ingredients":"dill, buttermilk, mayonnaise, dijon mustard"},{"name":"Crispy Tofu with Black Pepper, Ginger and Scallions on Rice Noodles","ingredients":"ginger, soy sauce, scallions, freshly ground black pepper, rice, garlic, vegetable oil, salt"},{"name":"Pineapple And Chicken Sandwiches Recipe","ingredients":"pecans, cream cheese, boned chicken, white, tarragon, pineapple"},{"name":"Streusel Jam Tart Recipe","ingredients":"sugar, oats, brown sugar, baking soda, strawberry preserves, flour, kosher salt, almonds, unsalted butter"},{"name":"Potato-Crusted Catfish And Chips","ingredients":"catfish fillets, pepper, yellow cornmeal, vegetable oil, butter, baking potatoes, salt"}]""");
        var selected = JsonSerializer.Deserialize<IEnumerable<string>>("""["Asian Taro Tapioca Dessert Soup","Potato-Crusted Catfish And Chips"]""");

        IEnumerable<string?> selectedMenus = menus.RootElement
                .EnumerateArray()
                .Where(
                    x => selected.Contains(x.GetProperty("name").GetString()))
                .SelectMany(x => x.GetProperty("ingredients").GetString().Split(", "))
                .Distinct();

        Console.WriteLine(string.Join(", ", selectedMenus));
    }
}
