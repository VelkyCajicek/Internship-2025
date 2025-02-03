using Plots

# For heatmaps
# https://docs.juliaplots.org/dev/generated/colorschemes/

# Julia indexes from 1 :/
function generate_test_case()
    points_x = [k/32 for k in 0:31]
    points_y = [7*k/32 for k in 0:31]
    for i in 1:length(points_x)-1
        points_x[i] = round(points_x[i] % 1, digits=4)
        points_y[i] = round(points_y[i] % 1, digits=4)
    end
    return points_x, points_y
end

function main()
    points_x, points_y = generate_test_case()
    plot(points_x, points_y)
end

main()