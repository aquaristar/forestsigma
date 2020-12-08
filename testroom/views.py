from django.shortcuts import render, redirect
from .models import *
# Create your views here.

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_test(my_ip):
	try:
		test = Test.objects.filter(value=0).get(user_ip=my_ip)		
	except Test.DoesNotExist:
		test = None
	
	if not test:
		test = Test.objects.create(user_ip=my_ip)

	return test

def get_test_item(test_id):
	try:
		test_item = None
		test_item = TestItem.objects.filter(test_id=test_id).order_by('-item_id')
		if test_item:
			test_item = test_item[0]		
	except TestItem.DoesNotExist:
		test_item = None
	return test_item

def get_item_list(sequence):
	item_list = []
	for idx in range(sequence, 397, 11):
		item_list.append(Item.objects.get(item_id=idx))
	return item_list

def index(request):	
	my_ip = get_client_ip(request)
	current_test = get_test(my_ip)
	sequence = 1
	submit_button_flag = False
	if request.method == 'POST':
		print('sequence:' + request.POST['sequence'])
		sequence = int(request.POST['sequence'])		
		for idx in range(1,37):
			print('select_item:' + str(idx) + " ==  " + request.POST['select_item_'+str(idx)])
			item_id = int(range(sequence, 397, 11)[idx-1])
			print (item_id)
			obj, created = TestItem.objects.get_or_create(
				test_id=current_test, 
				item_id=Item.objects.get(item_id=item_id), 
				choice_id=ItemChoice.objects.get(choice_id=request.POST['select_item_'+str(idx)]))
			if not created:
				print ("Test Item is already there")
	
	current_max_test_item = get_test_item(current_test.test_id)	
	if current_max_test_item:
		print(current_max_test_item.item_id.item_id)
		sequence = int(current_max_test_item.item_id.item_id) % 11 + 1
		if sequence == 11:
			submit_button_flag = True
		if sequence == 1:
			return test_result(request)
	current_sequence = get_item_list(sequence)
	subscale_list = Subscale.objects.all()
	
	data_list = zip(subscale_list, current_sequence)
	return render(request, 'testroom.html', {'data_list':data_list, 'sequence':sequence, 'submit':submit_button_flag})


def calc_test_result():
	return 100

def test_result(request):
	my_ip = get_client_ip(request)
	current_test = get_test(my_ip)
	test_result = calc_test_result()
	current_test.value = test_result
	current_test.save()
	test_item_list = TestItem.objects.filter(test_id=current_test.test_id)
	return render(request, 'test_result.html', {'test_result':test_result, 'test_item_list':test_item_list})


def admin(request):
	test_list = Test.objects.all()
	return render(request, 'test_admin.html', {'test_list':test_list})

def test_detail(request, test_id):
	test_item_list = TestItem.objects.filter(test_id=test_id)
	return render(request, 'test_detail.html', {'test_id':test_id, 'test_item_list':test_item_list})

def test_delete(request, test_id):
	Test.objects.get(pk=test_id).delete()
	return redirect('/test/admin')
