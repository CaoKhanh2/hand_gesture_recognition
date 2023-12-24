def read_file(file_path):
    result_dict = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Chia dòng thành các phần bằng dấu cách
                parts = line.strip().split(' ')

                # Kiểm tra xem có đủ phần tử trong danh sách hay không
                if len(parts) >= 2:
                    key = parts[0]
                    value = int(parts[1])
                    result_dict[key] = value

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return result_dict
