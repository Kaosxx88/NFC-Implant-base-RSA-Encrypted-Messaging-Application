#if defined(HAVE_CONFIG_H)
    #include "config.h"
#endif

#include <err.h>
#include <errno.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <nfc/nfc.h>

#include <freefare.h>

/* key version */

#define NEW_KEY_VERSION 0x01

struct {
    bool interactive;
} configure_options = {
    .interactive = true
};


int
create_application(nfc_device *device, MifareDESFireKey master_key_card_loaded, MifareDESFireAID aid_app, MifareDESFireKey new_key_app, int file_size, uint8_t file_id)
{	
		int error = EXIT_SUCCESS;
		FreefareTag *tags = NULL; 
		
		tags = freefare_get_tags(device);

		if (!tags) {
		    nfc_close(device);
		    errx(EXIT_FAILURE, "Error listing Mifare DESFire tags.");
		}

		for (int i = 0; (!error) && tags[i]; i++) {
	    if (MIFARE_DESFIRE != freefare_get_tag_type(tags[i]))
		continue;

	    char *tag_uid = freefare_get_tag_uid(tags[i]);
	    char buffer[BUFSIZ];

	    int res;

	    res = mifare_desfire_connect(tags[i]);
	    if (res < 0) {
		warnx("Can't connect to Mifare DESFire target.");
		error = EXIT_FAILURE;
		break;
	    }

	    // Make sure we've at least an EV1 version
	    struct mifare_desfire_version_info info;
	    res = mifare_desfire_get_version(tags[i], &info);
	    if (res < 0) {
		freefare_perror(tags[i], "mifare_desfire_get_version");
		error = 1;
		break;
	    }
	    if (info.software.version_major < 1) {
		warnx("Found old DESFire, skipping");
		continue;
	    }

	    printf("\nFound %s with UID %s. \n", freefare_get_tag_friendly_name(tags[i]), tag_uid);
	    bool do_it = true;

	    if (configure_options.interactive) {
		printf("\nCreating application and changing the AMK, Ready to proceed? [yN] ");
		fgets(buffer, BUFSIZ, stdin);
		do_it = ((buffer[0] == 'y') || (buffer[0] == 'Y'));
	    } else {
		printf("\n");
	    }

	    if (do_it) {

	    /* Authenticate the card with the card master key*/
	    /* Card master key*/

	    

		
		res = mifare_desfire_authenticate(tags[i], 0, master_key_card_loaded);
		if (res < 0) {
		    freefare_perror(tags[i], "mifare_desfire_authenticate");
		    error = EXIT_FAILURE;
		    break;
		}

		printf("\nCard authenticated\n");
		//

		/* ################################# SETTING APPLICATION 999999 ################################################ */

		/* Application master key */
		

		
		mifare_desfire_key_set_version(new_key_app, NEW_KEY_VERSION);
		res = mifare_desfire_set_default_key(tags[i], new_key_app);
		free(new_key_app);
		if (res < 0) {
		    freefare_perror(tags[i], "mifare_desfire_set_master_key");
		    error = EXIT_FAILURE;
		    break;
		}

		printf("\nNew Application master key loaded\n");

		/*
		 * Perform some tests to ensure the function actually worked
		 * (it's hard to create a unit-test to do so).
		 */

		
		res = mifare_desfire_create_application(tags[i], aid_app, 0xFF, 1);

		if (res < 0) {
		    freefare_perror(tags[i], "mifare_desfire_create_application");
		    error = EXIT_FAILURE;
		    break;
		}

		printf("\nApplication Created\n");

		res = mifare_desfire_select_application(tags[i], aid_app);
		if (res < 0) {
		    freefare_perror(tags[i], "mifare_desfire_select_application");
		    error = EXIT_FAILURE;
		    break;
		}

		uint8_t version_key_app_1;
		res = mifare_desfire_get_key_version(tags[i], 0, &version_key_app_1);
		if (res < 0) {
		    freefare_perror(tags[i], "mifare_desfire_get_key_version");
		    error = EXIT_FAILURE;
		    break;
		}


		if (version_key_app_1 != NEW_KEY_VERSION) {
		    fprintf(stderr, "Wrong key version: %02x (expected %02x).\n", version_key_app_1, NEW_KEY_VERSION);
		    error = EXIT_FAILURE;
		    /* continue */
		}






		res = mifare_desfire_authenticate(tags[i], 0, new_key_app);




		if (res < 0) {
		    freefare_perror(tags[i], "mifare_desfire_authenticate");
		    error = EXIT_FAILURE;
		    break;
		}

		printf("\nApplication Done\n");

		

		printf("\nCreating the file\n");

   		res = mifare_desfire_create_std_data_file(tags[i], file_id, MDCM_PLAIN, 0x00E0, file_size);

		/* ######################################################################################## */


		printf("\nNew application master key correctly loaded in the app and file created\n");


	    }

	    mifare_desfire_disconnect(tags[i]);

	    free(tag_uid);



	    freefare_free_tags(tags);
	}


}



int 
change_card_master_key(nfc_device *device, MifareDESFireKey old_card_master_key,  MifareDESFireKey new_card_master_key)
{
		int error = EXIT_SUCCESS;
		FreefareTag *tags = NULL; 
		
		tags = freefare_get_tags(device);

		if (!tags) {
		    nfc_close(device);
		    errx(EXIT_FAILURE, "Error listing Mifare DESFire tags.");
		}

		for (int i = 0; (!error) && tags[i]; i++) {
	    if (MIFARE_DESFIRE != freefare_get_tag_type(tags[i]))
		continue;

	    char *tag_uid = freefare_get_tag_uid(tags[i]);
	    char buffer[BUFSIZ];

	    int res;

	    res = mifare_desfire_connect(tags[i]);
	    if (res < 0) {
		warnx("Can't connect to Mifare DESFire target.");
		error = EXIT_FAILURE;
		break;
	    }

	    // Make sure we've at least an EV1 version
	    struct mifare_desfire_version_info info;
	    res = mifare_desfire_get_version(tags[i], &info);
	    if (res < 0) {
		freefare_perror(tags[i], "mifare_desfire_get_version");
		error = 1;
		break;
	    }
	    if (info.software.version_major < 1) {
		warnx("Found old DESFire, skipping");
		continue;
	    }

	    printf("\nFound %s with UID %s. \n", freefare_get_tag_friendly_name(tags[i]), tag_uid);
	    bool do_it = true;

	    if (configure_options.interactive) {
		printf("\nChanging the Card Master Key, ready to proceed? [yN] ");
		fgets(buffer, BUFSIZ, stdin);
		do_it = ((buffer[0] == 'y') || (buffer[0] == 'Y'));
	    } else {
		printf("\n");
	    }

	    if (do_it) {




	    res = mifare_desfire_authenticate(tags[i], 0, old_card_master_key);
		if (res < 0) {
			printf("\nAuthentication faliture\n");
		    error = EXIT_FAILURE;
		    break;
		}


		printf("\nCard Master key Authetication ok\n");

	    mifare_desfire_change_key(tags[i], 0, new_card_master_key, old_card_master_key);

		if (res < 0) {
			printf("\nChange key faliture\n");
		    error = EXIT_FAILURE;
		    break;
		}
		
		printf("\nCard MAster key Changed \n");


	}}
}

int
main()
{	

	printf("\nStarting Application\n");

	/* Actual Card Master key */
	uint8_t master_key_card[8]  = { 0x99, 0x99, 0x99, 0x99, 0x99, 0x99, 0x99, 0x99 }; 

	/* New Card Master key */
	uint8_t new_master_key_card[8]  = { 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22 };

	/* Application 1 master key */
	uint8_t app_1_master_key[8]  = { 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33 };

	/* Application 2 master key */
	uint8_t app_2_master_key[8]  = { 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33 };	

	/* Application 1 number / Name */
	MifareDESFireAID aid_app_1 =  mifare_desfire_aid_new(0x999999);

	/* Application 2 Number / Name */
	MifareDESFireAID aid_app_2= mifare_desfire_aid_new(0x888888);

	int file_size_app_1 = 3312;

	int file_size_app_2 = 800;

	uint8_t file_id_app_1 = 01;

	uint8_t file_id_app_2 = 01;


	/* ################################################################################### */


	MifareDESFireKey master_key_card_loaded = mifare_desfire_des_key_new_with_version(master_key_card);

	MifareDESFireKey new_key_app_1 = mifare_desfire_des_key_new(app_1_master_key);

	MifareDESFireKey new_key_app_2 = mifare_desfire_des_key_new(app_2_master_key);		

	MifareDESFireKey old_card_master_key = mifare_desfire_des_key_new(master_key_card);
	    
	MifareDESFireKey new_card_master_key = mifare_desfire_des_key_new(new_master_key_card);



	


    int ch;
    int error = EXIT_SUCCESS;
    nfc_device *device = NULL;
       
   

    nfc_connstring devices[8];
    size_t device_count;

    nfc_context *context;
    nfc_init(&context);
    if (context == NULL)
	errx(EXIT_FAILURE, "Unable to init libnfc (malloc)");

    device_count = nfc_list_devices(context, devices, 8);
    if (device_count <= 0)
	errx(EXIT_FAILURE, "No NFC device found.");

    for (size_t d = 0; (!error) && (d < device_count); d++) {
	device = nfc_open(context, devices[d]);
	if (!device) {
	    warnx("nfc_open() failed.");
	    error = EXIT_FAILURE;
	    continue;
	}


	// calling the functions

	// Creating aid_app_1 with new_key_app_1 (999999)
	create_application(device, master_key_card_loaded, aid_app_1, new_key_app_1, file_size_app_1, file_id_app_1);

	// Creating aid_app_2 with new_key_app_2 (888888)
	create_application(device, master_key_card_loaded, aid_app_2, new_key_app_2, file_size_app_2, file_id_app_1);

	// Change the Card Master Key
	//change_card_master_key(device, old_card_master_key,  new_card_master_key);


	mifare_desfire_key_free(master_key_card_loaded);

	nfc_close(device);

	printf("\nProcess completed...\n");
    }
    nfc_exit(context);

}


// Create files in the application A
//    res = mifare_desfire_select_application(tag, aid_a);
//    cut_assert_success("mifare_desfire_select_application()");
//
//    uint8_t std_data_file_id = 15;

   // res = mifare_desfire_create_std_data_file(tag, std_data_file_id, MDCM_PLAIN, 0xEEEE, 100);