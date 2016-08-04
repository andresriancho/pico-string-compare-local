require 'active_support'

SAMPLES = 5000

tests = []

File.open('../tests.csv').each do |line|
    line = line.strip()
    parts = line.split(',')
    tests << parts
end

def naive_strcmp(str_a, str_b)
    if str_a.size != str_b.size
        return false
    end

    str_a.size.times { |i|
        if str_a[i] != str_b[i]
            return false
        end
    }

    return true
end

measurements = ActiveSupport::OrderedHash.new
tests.each do |str_test|
    measurements[str_test[1]] = 0.0
end

SAMPLES.times do

    # TODO: Shuffle with the same random seed?
    tests = tests.shuffle

    tests.each do |str_test|
        str_a = str_test[0]
        str_b = str_test[1]

        start_time = Time.now.nsec

        # Compare the test strings
        # str_a == str_b
        naive_strcmp(str_a, str_b)

        end_time = Time.now.nsec
        spent_time = end_time - start_time
        
        if spent_time < 0
            puts "Go home Ruby, you're drunk. Negative time spent: #{spent_time}"
            next
        end
        
        measurements[str_b] += end_time - start_time
    end
end

# A * 128
base_string = tests[0][0]

measurements.keys.each do |str_b|
    puts "#{base_string},#{str_b},#{SAMPLES},#{measurements[str_b]}"
end
