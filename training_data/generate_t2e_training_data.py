import json
import random

# Base translation pairs (Tagalog ↔ English)
base_pairs = [
    # Greetings & Introductions
    ("Kamusta ka?", "How are you?"),
    ("Magandang umaga!", "Good morning!"),
    ("Magandang gabi!", "Good evening!"),
    ("Magandang hapon!", "Good afternoon!"),
    ("Anong pangalan mo?", "What is your name?"),
    ("Ako si [Name].", "I am [Name]."),
    ("Ikinagagalak kitang makilala.", "Nice to meet you."),
    ("Paalam!", "Goodbye!"),
    ("Hanggang sa muli!", "Until next time!"),

    # Personal Questions
    ("Ilang taon ka na?", "How old are you?"),
    ("Saan ka nakatira?", "Where do you live?"),
    ("Anong trabaho mo?", "What is your job?"),
    ("May pamilya ka ba?", "Do you have a family?"),
    ("May anak ka ba?", "Do you have children?"),
    ("May alaga kang hayop?", "Do you have a pet?"),

    # Feelings & Emotions
    ("Masaya ako.", "I am happy."),
    ("Malungkot ako.", "I am sad."),
    ("Galit ka ba?", "Are you angry?"),
    ("Naiinip ako.", "I am bored."),
    ("Natatakot ako.", "I am scared."),
    ("Kinakabahan ako.", "I am nervous."),
    ("Excited ako!", "I am excited!"),
    ("Pagod na ako.", "I am tired."),

    # Likes / Dislikes / Preferences
    ("Gusto ko ng kape.", "I like coffee."),
    ("Ayaw ko ng tsaa.", "I don't like tea."),
    ("Anong paborito mong pagkain?", "What is your favorite food?"),
    ("Mahilig ako sa musika.", "I love music."),
    ("Gusto mo ba ng prutas?", "Do you like fruit?"),

    # Common Phrases
    ("Mahal kita.", "I love you."),
    ("Pasensya na.", "Sorry."),
    ("Walang anuman.", "You're welcome."),
    ("Salamat!", "Thank you!"),
    ("Maraming salamat!", "Thank you very much!"),
    ("Wala akong alam.", "I don't know."),
    ("Totoo ba?", "Is it true?"),
    ("Hindi ako sigurado.", "I'm not sure."),
    ("Teka lang.", "Wait a moment."),
    ("Sige.", "Alright."),
    ("Tara na!", "Let's go!"),
    ("Halika dito.", "Come here."),
    ("Ingat ka.", "Take care."),
    ("Anong oras na?", "What time is it?"),

    # Directions & Places
    ("Saan ang banyo?", "Where is the bathroom?"),
    ("Nasaan ang ospital?", "Where is the hospital?"),
    ("Paano pumunta sa palengke?", "How do I get to the market?"),
    ("Saan ang terminal ng jeep?", "Where is the jeep terminal?"),
    ("Malayo ba ito?", "Is it far?"),
    ("Malapit lang.", "It's just nearby."),
    ("Kaliwa o kanan?", "Left or right?"),

    # Time / Date
    ("Anong araw ngayon?", "What day is it today?"),
    ("Anong petsa na?", "What is the date?"),
    ("Kailan ang kaarawan mo?", "When is your birthday?"),
    ("Anong oras ang klase mo?", "What time is your class?"),
    ("Gabi na ba?", "Is it already night?"),

    # Food & Drink
    ("Kumain ka na ba?", "Have you eaten?"),
    ("Anong gusto mong kainin?", "What do you want to eat?"),
    ("Busog na ako.", "I'm full."),
    ("Gutom na ako.", "I'm hungry."),
    ("Gusto mo ng tubig?", "Do you want water?"),
    ("Masarap ba ito?", "Is this delicious?"),
    ("Ano ang ulam?", "What's the dish?"),

    # Conversations / Requests
    ("May tanong ako.", "I have a question."),
    ("Pwede ba kitang tanungin?", "Can I ask you something?"),
    ("Saan ka pupunta?", "Where are you going?"),
    ("Bakit ka umiiyak?", "Why are you crying?"),
    ("Anong ginagawa mo?", "What are you doing?"),
    ("Anong ibig mong sabihin?", "What do you mean?"),
    ("Pakiulit nga.", "Please repeat."),
    ("Pakihinaan ang boses mo.", "Please lower your voice."),
    ("Pakibilisan mo.", "Please hurry."),
    ("Tama na.", "That's enough."),

    # Technology / Daily Life
    ("Nasaan ang cellphone ko?", "Where is my phone?"),
    ("Wala akong signal.", "I have no signal."),
    ("Mabagal ang internet.", "The internet is slow."),
    ("Panoorin natin ito.", "Let's watch this."),
    ("Nanonood ako ng pelikula.", "I'm watching a movie."),
    ("Naglalaro ako ng video game.", "I'm playing a video game."),
    ("Nagcha-chat ako.", "I'm chatting."),
    ("Nagpapahinga lang ako.", "I'm just resting."),

    # Weather / Environment
    ("Mainit ngayon.", "It's hot today."),
    ("Umuulan ba?", "Is it raining?"),
    ("Malamig sa labas.", "It's cold outside."),
    ("Maaraw ngayon.", "It's sunny today."),
    ("Maulan buong araw.", "It rained all day."),

    # Daily Activities
    ("Naglalakad ako sa parke.", "I am walking in the park."),
    ("Nagluluto ako ng hapunan.", "I am cooking dinner."),
    ("Nagbabasa ako ng libro.", "I am reading a book."),
    ("Naliligo ako.", "I am taking a shower."),
    ("Natutulog na ako.", "I am going to sleep."),
    ("Nanonood ako ng TV.", "I am watching TV."),
    ("Naglalaba ako ngayon.", "I am doing the laundry."),
    ("Nagwawalis ako ng sahig.", "I am sweeping the floor."),

    # School / Learning
    ("Papasok ako sa paaralan.", "I am going to school."),
    ("Tapos na ang klase ko.", "My class is over."),
    ("Nagtuturo ang guro.", "The teacher is teaching."),
    ("Nag-aaral ako ng Tagalog.", "I am studying Tagalog."),
    ("Anong subject mo ngayon?", "What subject do you have now?"),
    ("Mahilig ako sa Math.", "I like Math."),
    ("Ayoko ng Science.", "I don’t like Science."),
    ("May assignment ka ba?", "Do you have homework?"),

    # Work / Office
    ("Papasok ako sa opisina.", "I'm going to the office."),
    ("Trabaho muna ako.", "I have to work first."),
    ("May meeting ako mamaya.", "I have a meeting later."),
    ("Nasa trabaho pa ako.", "I'm still at work."),
    ("Day off ko ngayon.", "Today is my day off."),
    ("OT ako ngayon.", "I'm working overtime today."),
    ("Late na ako sa opisina.", "I'm late for the office."),
    ("Anong trabaho mo?", "What is your job?"),

    # Transportation
    ("Sumasakay ako ng jeep.", "I'm riding a jeepney."),
    ("Nasa bus ako ngayon.", "I'm on the bus now."),
    ("Nag-aabang ako ng taxi.", "I'm waiting for a taxi."),
    ("Saan ang sakayan papuntang Cubao?", "Where's the ride going to Cubao?"),
    ("Traffic sa EDSA.", "There's traffic on EDSA."),
    ("Bumaba ka na ba?", "Have you gotten off?"),
    ("Saan ang terminal ng tricycle?", "Where is the tricycle terminal?"),
    ("Pwedeng makisabay?", "Can I ride with you?"),

    # Weather & Environment
    ("Ang lakas ng ulan.", "It's raining hard."),
    ("Maaraw buong araw.", "It’s sunny all day."),
    ("Lumindol ba kanina?", "Did it just quake?"),
    ("May bagyo ngayon.", "There's a storm today."),
    ("Mahangin sa labas.", "It's windy outside."),
    ("Umulan ng yelo sa Baguio.", "It hailed in Baguio."),
    ("Mainit ang panahon ngayon.", "The weather is hot today."),
    ("Malamig sa Tagaytay.", "It's cold in Tagaytay."),

    # Shopping & Money
    ("Magkano ito?", "How much is this?"),
    ("Saan ang pinakamalapit na mall?", "Where is the nearest mall?"),
    ("Pahingi ng resibo.", "Can I have a receipt?"),
    ("May discount ba ito?", "Does this have a discount?"),
    ("Anong size mo?", "What's your size?"),
    ("Cash o card?", "Cash or card?"),
    ("Wala akong pera.", "I don't have money."),
    ("Saan ako pwedeng magbayad?", "Where can I pay?"),

    # Health & Feelings
    ("Masakit ang ulo ko.", "I have a headache."),
    ("Nilalagnat ako.", "I have a fever."),
    ("Masakit ang tiyan ko.", "My stomach hurts."),
    ("May gamot ka ba?", "Do you have medicine?"),
    ("Pagod na ako.", "I'm already tired."),
    ("Nangangati ang balat ko.", "My skin is itchy."),
    ("Nadulas ako kanina.", "I slipped earlier."),
    ("Nasa ospital siya ngayon.", "He/She is in the hospital now."),

    # Technology & Internet
    ("Walang signal dito.", "There’s no signal here."),
    ("Mabagal ang Wi-Fi.", "The Wi-Fi is slow."),
    ("Nasaan ang charger ko?", "Where is my charger?"),
    ("Lowbat na ako.", "My battery is low."),
    ("Nag-download ako ng app.", "I downloaded an app."),
    ("Wala akong load.", "I don’t have load."),
    ("Nag-update ako ng software.", "I updated the software."),
    ("Nagka-error ang system.", "The system had an error."),

    # Emotions & Reactions
    ("Ang saya ko ngayon!", "I'm so happy today!"),
    ("Na-stress ako sa trabaho.", "I'm stressed from work."),
    ("Naiiyak na ako.", "I’m about to cry."),
    ("Nakakatawa yan!", "That’s funny!"),
    ("Naiinis na ako.", "I'm getting annoyed."),
    ("Kinilig ako doon.", "That made me feel giddy."),
    ("Nakakahiya naman.", "That’s embarrassing."),
    ("Nagulat ako!", "I was surprised!"),

    # Expressions / Idioms
    ("Bahala na si Batman.", "Whatever happens, happens."),
    ("Nagbibilang ng poste.", "Unemployed."),
    ("Walang himala!", "There is no miracle!"),
    ("Kapag may tiyaga, may nilaga.", "If there's perseverance, there's reward."),
    ("Nagpapanggap kang may alam.", "You're pretending to know."),
    ("Anong petsa na?!", "What the heck is taking so long?!"),
    ("Suntok sa buwan.", "A shot in the dark."),
    ("Hindi ko na kaya.", "I can't take it anymore."),

    # Yes / No / Clarifications
    ("Oo.", "Yes."),
    ("Hindi.", "No."),
    ("Sigurado ka ba?", "Are you sure?"),
    ("Totoo ba yan?", "Is that true?"),
    ("Pwede bang ulitin mo?", "Can you repeat that?"),
    ("Paki-type sa chat.", "Please type it in the chat."),
    ("Hindi ko maintindihan.", "I don’t understand."),
    ("Mali yata ang sinabi mo.", "I think you said it wrong."),

    # Events & Plans
    ("May party mamaya.", "There’s a party later."),
    ("Pupunta ka ba sa event?", "Are you going to the event?"),
    ("Sino ang kasama mo?", "Who are you with?"),
    ("Anong plano mo sa weekend?", "What's your plan for the weekend?"),
    ("Bukas na ang outing.", "The outing is tomorrow."),
    ("Late ako dumating.", "I arrived late."),
    ("Nagkita kami sa mall.", "We met at the mall."),
    ("Nag-date kami kahapon.", "We went on a date yesterday."),
]


# Generate a million samples
def generate_translation_samples(pairs, n_samples=250000):
    samples = []
    for _ in range(n_samples // 2):
        tagalog, english = random.choice(pairs)
        samples.append({"prompt": tagalog, "completion": english})
        samples.append({"prompt": english, "completion": tagalog})
    return samples

# Create the dataset
def generate():
    samples = generate_translation_samples(base_pairs, n_samples=250000)

    # Save to JSONL file
    output_file = "train_t2e.jsonl"
    with open(output_file, "w", encoding="utf-8") as f:
        for sample in samples:
            json.dump(sample, f, ensure_ascii=False)
            f.write("\n")

    print(f"Generated {len(samples)} samples to '{output_file}'")