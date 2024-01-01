from connect import connectDB
from pymongo import errors
from matches import match_data
from reviews import review_data
import json
from bson.objectid import ObjectId

#prepared by Eren Cavus and Tuna Dagdanas


def createCollection(db, collection_name):
    try:
        if collection_name not in db.list_collection_names():
            db.create_collection(collection_name)
            print(f"Collection '{collection_name}' created.")
        elif collection_name in db.list_collection_names():
            print("Collection already exists")
    except Exception as e:
        print("An error occured: ", e)


def insert_into_collection(db, collection_name, data):
    try:
        collection = db[collection_name]

        result = collection.insert_one(data)

        print("Insertion successfully completed")
        print(f"Inserted document ID: {result.inserted_id}")

    except Exception as e:
        print(f"An error occurred: {e}")


def read_all_data(db, collection_name):
    try:
        collection = db[collection_name]

        result = collection.find()

        for document in result:
            print(document)

    except Exception as e:
        print(f"An error occurred: {e}")


def find_orders_containing_item(db, collection_name, item_name,lhs):
    try:
        collection = db[collection_name]

        query = { lhs : item_name}

        cursor = collection.find(query)

        result = list(cursor)

        for document in result:
            print(document)

        return result

    except Exception as e:
        print(f"An error occurred: {e}")


def delete_record_by_id(db, collection_name, record_id):
    try:
        collection = db[collection_name]

        item_id = ObjectId(record_id)

        query = {"_id": item_id}

        result = collection.delete_one(query)

        if result.deleted_count == 1:
            print(f"Successfully deleted record with ID {record_id}")
        else:
            print(f"No record found with ID {record_id}")

    except errors.PyMongoError as e:
        print(f"An error occurred: {e}")


def update_by_id(db, collection_name, record_id, lhs, rhs ):
    try:
        collection = db[collection_name]
        item_id = ObjectId(record_id)

        query = {"_id": item_id}

        result = collection.update_one(query, {"$set": {lhs: rhs}})

        if result.matched_count == 1:
            print(f"Successfully updated ", rhs ," for record with ID {record_id}")
        else:
            print(f"No record found with ID {record_id}")

    except errors.PyMongoError as e:
        print(f"An error occurred: {e}")


def delete_record_by_item(db, collection_name, item="Pizza"):
    try:
        collection = db[collection_name]

        query = {"order_items.item_name": item}

        result = collection.delete_many(query)

        if result.deleted_count >= 1:
            print(
                f"Successfully deleted {result.deleted_count} record that contains {item}"
            )
        else:
            print(f"No record found with {item}")

    except errors.PyMongoError as e:
        print(f"An error occurred: {e}")


def list_collection(db):
    print("\n")
    num = 1
    print("Please select the collection : ")
    for collection in db.list_collection_names():
        print(num,"-",collection)
        num += 1    
    
    print("\n")

def select_collection(db, i):
    num = 1
    dummy = ""  
    for collection in db.list_collection_names():
        #print(num,"-",collection)
        if(num == i):
            #print("\nhere\n")
            dummy = collection
        num += 1

    #print("---------->",dummy)
    return dummy

def get_all_field_names(db, collection_name):
    collection = db[collection_name]
    field_names = set()

    for document in collection.find():
        field_names.update(document.keys())

    return list(field_names)


def gather_data(db, field_names):
    # Get all field names in the collection

    # Gather data from the user
    data = {}
    for field_name in field_names:
        if(field_name != "_id"):
            data[field_name] = input(f"Enter the value for '{field_name}': ")

    return data


def user_interface(db):
    print("Welcome to Review Portal!")
    user_id = input("Please enter your user id: ")
    while True:
        #print("Welcome to Review Portal!")
        #user_id = input("Please enter your user id: ")

        print("Please pick the option that you want to proceed:")
        print("1- Create a collection.")
        print("2- Read all data in a collection.")
        print("3- Read some part of the data while filtering.")
        print("4- Insert data.")
        print("5- Delete data.")
        print("6- Update data.")
        print("7- Exit.")
        print()
        selected_option = input("Selected option: ")

        if selected_option == "1":
            collection_name = input("Enter the collection name: ")
            createCollection(db, collection_name)
            print("\n")

        elif selected_option == "2":
            list_collection(db)
            collection_num = int(input("Enter the collection number: "))
            collection_name = select_collection(db, collection_num)
            #print(collection_name)
            print("\n")
            read_all_data(db, collection_name)
            print("\n")

        elif selected_option == "3":
            list_collection(db)
            collection_num = int(input("Enter the collection number: "))
            collection_name = select_collection(db, collection_num)
            print() 
            print("Fields: ",get_all_field_names(db, collection_name))
            lhs_name = input("Enter the attribute to filter: ")
            rhs_name = input("Enter the attribute name to filter: ")
            print("\n")
            find_orders_containing_item(db, collection_name, rhs_name,lhs_name)
            print("\n")


        elif selected_option == "4":
            list_collection(db)
            collection_num = int(input("Enter the collection number: "))
            collection_name = select_collection(db, collection_num)
            fieldNames = get_all_field_names(db, collection_name)
            data = gather_data(db, fieldNames)
            insert_into_collection(db, collection_name, data)
            print("\n")



        elif selected_option == "5":
            list_collection(db)
            collection_num = int(input("Enter the collection number: "))
            collection_name = select_collection(db, collection_num)
            record_id = input("Enter the record ID to delete: ")
            delete_record_by_id(db, collection_name, record_id)
            print("\n")

        elif selected_option == "6":
            list_collection(db)
            collection_num = int(input("Enter the collection number: "))
            collection_name = select_collection(db, collection_num)
            
            record_id = input("Enter the record ID to update: ")
            lhs_name = input("Enter the attribute to update: ")
            rhs_name = input("Enter the attribute name to update: ")
            update_by_id(db, collection_name, record_id, lhs_name, rhs_name)
            print("\n")



        elif selected_option == "7":
            print("Exiting the Review Portal.")
            break
        else:
            print("Invalid option. Please select again.")




if __name__ == "__main__":
    db = connectDB()
    user_interface(db)

    #createCollection(db, "matches")
    #createCollection(db, "reviews")

    # # Insert some dummy data into your collection
    #for item in match_data:
        #insert_into_collection(db, "matches", item)
    #for item in review_data:
        #insert_into_collection(db, "reviews", item)
    
    #read_all_data(db, "reviews")


   # 
   #print(get_all_field_names(db, "matches"))

    #print(gather_data(db, get_all_field_names(db, "matches")))



    

    #found_documents = find_orders_containing_item(
        #db,collection_name="reviews", item_name=7, lhs="review_id"
    #)
    
    #id_to_delete = found_documents[0]["_id"]
    #print(type(id_to_delete))
    #delete_record_by_id(db, "reviews", id_to_delete)

    #found_documents = find_orders_containing_item(
        #db,collection_name="reviews", item_name=4, lhs="given_rating"
    #)


